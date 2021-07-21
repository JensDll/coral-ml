using Application.Data.DataTransfer.Record;
using Contracts.Request;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

namespace Application.Mapping.Record
{
    public interface IRecordRequestMapper
    {
        Pagination MapPaginationRequest(PaginationRequestDto paginationRequestDto);

        Task<RecordCreate> MapCreateRequestAsync(int recordTypeId, IFormFile model, IFormFile label);
    }
}
