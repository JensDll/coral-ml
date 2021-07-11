using Application.Data.Models;
using Application.Mapping.Model;
using Contracts.Request;
using Contracts.Response;
using Domain.DataTransfer;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System.Linq;

namespace Infrastructure.Mapping.Model
{
    internal class TFLiteRecordRequestMapper : ITFLiteRecordRequestMapper
    {
        public FormFileZipper MapCreateRequest(IFormFile model, IFormFile label)
        {
            var modelEntry = new FormFileZipEntry
            {
                EntryName = "model.tflite",
                File = model
            };

            var labelEntry = new FormFileZipEntry
            {
                EntryName = "label.txt",
                File = label
            };

            return new FormFileZipper(modelEntry, labelEntry);
        }

        public Pagination MapPaginationRequest(PaginationRequestDto paginationRequestDto)
        {
            return new Pagination(paginationRequestDto.PageNumber,
                paginationRequestDto.PageSize);
        }
    }
}
