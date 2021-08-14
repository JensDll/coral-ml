using Application.Data.DataTransfer.Record;
using Application.Mapping.Record;
using Contracts.Request;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace Infrastructure.Mapping.Record
{
    internal class RecordRequestMapper : IRecordRequestMapper
    {
        public async Task<RecordCreate>
            MapCreateRequestAsync(int recordTypeId, IFormFile model, IFormFile label)
        {
            var zipEntries = new List<FormFileZipEntry>
            {
                new FormFileZipEntry
                {
                    EntryName = "model.tflite",
                    File = model
                }            
            };

            if (label != null)
            {
                zipEntries.Add(new FormFileZipEntry
                {
                    EntryName = "label",
                    File = label
                });
            }

            var zipper = new FormFileZipper(zipEntries.ToArray());

            byte[] zipContent = await zipper.CreateZipAsync();

            return new RecordCreate
            {
                ModelFileName = Path.GetFileName(model.FileName),
                ZipContent = zipContent,
                RecordTypeId = recordTypeId
            };
        }

        public Pagination MapPaginationRequest(PaginationRequestDto paginationRequestDto)
        {
            return new Pagination(paginationRequestDto.PageNumber,
                paginationRequestDto.PageSize);
        }
    }
}
